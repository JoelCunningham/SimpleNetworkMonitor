import { DevicePortInformation } from '#components/form-sections';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('DevicePortInformation', () => {
  let component: DevicePortInformation;
  let fixture: ComponentFixture<DevicePortInformation>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DevicePortInformation],
    }).compileComponents();

    fixture = TestBed.createComponent(DevicePortInformation);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
