import { EditDeviceForm } from '#components/forms';
import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('EditDeviceForm', () => {
  let component: EditDeviceForm;
  let fixture: ComponentFixture<EditDeviceForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditDeviceForm],
      providers: [provideHttpClient()],
    }).compileComponents();

    fixture = TestBed.createComponent(EditDeviceForm);
    component = fixture.componentInstance;
    component.device = {
      id: 1,
      name: 'Test Device',
      model: 'Test Model',
      category: { id: 1, name: 'Test Category' },
      location: { id: 1, name: 'Test Location' },
      owner: null,
      macs: [],
      primary_mac: {
        id: 1,
        address: '00:11:22:33:44:55',
        last_ip: '192.168.1.100',
        last_seen: '2024-01-01T00:00:00Z',
        hostname: 'test-host',
        vendor: 'Test',
        device: null,
        discoveries: [],
        ports: [],
      },
    };
    component.ngOnChanges();
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
