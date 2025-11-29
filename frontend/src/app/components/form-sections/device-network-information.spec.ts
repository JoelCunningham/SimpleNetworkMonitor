import { DeviceNetworkInformation } from '#components/form-sections';
import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('DeviceNetworkInformation', () => {
  let component: DeviceNetworkInformation;
  let fixture: ComponentFixture<DeviceNetworkInformation>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DeviceNetworkInformation],
      providers: [provideHttpClient()],
    }).compileComponents();

    fixture = TestBed.createComponent(DeviceNetworkInformation);
    component = fixture.componentInstance;

    // Set required input
    component.mac = {
      id: 1,
      address: '00:11:22:33:44:55',
      last_ip: '192.168.1.100',
      hostname: 'test-host',
      last_seen: '2024-01-01T00:00:00Z',
      device: null,
      discoveries: [],
      ports: [],
    };

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
